import os
import gc
import time
import logging
import torch

logger = logging.getLogger(__name__)
class ModelLoader:
    _instance = None
    _model = None
    _tokenizer = None
    _model_type = None
    _load_time = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_loaded(self) -> bool:
        return self._model is not None

    def get_model_info(self) -> dict:
        return {
            "loaded": self.is_loaded(),
            "model_type": self._model_type,
            "load_time_sec": self._load_time,
            "gpu_available": torch.cuda.is_available(),
            "vram_used_gb": (
                round(torch.cuda.memory_allocated() / 1e9, 2)
                if torch.cuda.is_available() else 0
            ),
        }

    def load(self, config: dict) -> bool:
        if self.is_loaded():
            logger.info("Model already loaded, skipping reload")
            return True

        mode = config.get("mode", "quantised")
        logger.info(f"Loading model in mode: {mode}")
        start = time.time()

        try:
            if mode == "gguf":
                success = self._load_gguf(config)
            else:
                success = self._load_transformers(config, mode)

            if success:
                self._load_time = round(time.time() - start, 2)
                logger.info(f"Model loaded in {self._load_time}s")
                return True
            return False

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False

    def _load_gguf(self, config: dict) -> bool:
        try:
            from llama_cpp import Llama
        except ImportError:
            logger.error("llama-cpp-python not installed. Run: pip install llama-cpp-python")
            return False

        gguf_path = config.get("gguf_path", "")
        if not os.path.exists(gguf_path):
            logger.error(f"GGUF file not found: {gguf_path}")
            return False

        logger.info(f"Loading GGUF: {gguf_path}")
        self._model = Llama(
            model_path=gguf_path,
            n_ctx=2048,
            n_threads=os.cpu_count() or 4,
            verbose=False,
        )
        self._tokenizer = None 
        self._model_type = "gguf"
        return True

    def _load_transformers(self, config: dict, mode: str) -> bool:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        except ImportError:
            logger.error("transformers not installed")
            return False

        base_model = config.get("base_model", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        quantization = config.get("quantization", "4bit")

        logger.info(f"Loading tokenizer: {base_model}")
        self._tokenizer = AutoTokenizer.from_pretrained(base_model)
        self._tokenizer.pad_token = self._tokenizer.eos_token

        # Set up quantization config
        bnb_config = None
        load_dtype = torch.float16

        if quantization == "4bit" and mode != "base":
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
        elif quantization == "8bit" and mode != "base":
            bnb_config = BitsAndBytesConfig(load_in_8bit=True)

        logger.info(f"Loading model: {base_model} (quant={quantization})")
        load_kwargs = {
            "device_map": "auto" if torch.cuda.is_available() else "cpu",
            "trust_remote_code": True,
        }
        if bnb_config:
            load_kwargs["quantization_config"] = bnb_config
        else:
            load_kwargs["torch_dtype"] = load_dtype

        self._model = AutoModelForCausalLM.from_pretrained(base_model, **load_kwargs)

        # Load LoRA adapter if fine-tuned
        if mode == "fine_tuned":
            adapter_path = config.get("adapter_path", "")
            if os.path.exists(adapter_path):
                try:
                    from peft import PeftModel
                    logger.info(f"Loading LoRA adapter: {adapter_path}")
                    self._model = PeftModel.from_pretrained(self._model, adapter_path)
                    logger.info("Adapter loaded")
                except Exception as e:
                    logger.warning(f"Could not load adapter: {e}. Using base weights.")
            else:
                logger.warning(f"Adapter not found at {adapter_path}, using base model")

        self._model_type = "transformers"
        return True

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        repetition_penalty: float = 1.1,
        do_sample: bool = True,
        stream: bool = False,
    ) -> str:
        if not self.is_loaded():
            raise RuntimeError("Model not loaded! Call load() first.")

        if self._model_type == "gguf":
            return self._generate_gguf(
                prompt, max_new_tokens, temperature, top_p, top_k
            )
        else:
            return self._generate_transformers(
                prompt, max_new_tokens, temperature, top_p, top_k,
                repetition_penalty, do_sample
            )

    def _generate_transformers(
        self, prompt, max_new_tokens, temperature, top_p, top_k,
        repetition_penalty, do_sample
    ) -> str:
        inputs = self._tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=1024
        )
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        input_len = inputs["input_ids"].shape[1]

        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature if do_sample else 1.0,
                top_p=top_p if do_sample else 1.0,
                top_k=top_k if do_sample else 0,
                repetition_penalty=repetition_penalty,
                do_sample=do_sample,
                pad_token_id=self._tokenizer.eos_token_id,
                use_cache=True,
            )

        new_token_ids = outputs[0][input_len:]
        return self._tokenizer.decode(new_token_ids, skip_special_tokens=True)

    def generate_stream(self, prompt: str, **kwargs):
        if not self.is_loaded():
            raise RuntimeError("Model not loaded!")

        if self._model_type == "gguf":
            for chunk in self._model(
                prompt,
                max_tokens=kwargs.get("max_new_tokens", 256),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.9),
                top_k=kwargs.get("top_k", 50),
                stop=["### Instruction:","### Input:","### Response:"],
                stream=True,
            ):
                yield chunk["choices"][0]["text"]
        else:
            from transformers import TextIteratorStreamer
            import threading

            inputs = self._tokenizer(
                prompt, return_tensors="pt", truncation=True, max_length=1024
            )
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}

            streamer = TextIteratorStreamer(
                self._tokenizer, skip_prompt=True, skip_special_tokens=True
            )

            gen_kwargs = {
                **inputs,
                "max_new_tokens": kwargs.get("max_new_tokens", 256),
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "do_sample": kwargs.get("do_sample", True),
                "pad_token_id": self._tokenizer.eos_token_id,
                "streamer": streamer,
            }

            thread = threading.Thread(target=self._model.generate, kwargs=gen_kwargs)
            thread.start()

            for token_text in streamer:
                yield token_text

            thread.join()

    def _generate_gguf(self, prompt, max_new_tokens, temperature, top_p, top_k) -> str:
        output = self._model(
            prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=["### Instruction:", "### Input:", "### Response:"]
        )
        return output["choices"][0]["text"]

    def unload(self):
        """Free model from memory"""
        self._model = None
        self._tokenizer = None
        self._model_type = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info("Model unloaded")
model_loader = ModelLoader()