const headers = document.querySelectorAll(".accordian-h");

headers.forEach(header => {
    header.addEventListener("click",()=>{

        const item = header.parentElement;

        document.querySelectorAll(".accordian-item").forEach(el=>{
            if(el!==item){
                el.classList.remove("active");
                el.querySelector(".icon").textContent="+";
            }
        });

        item.classList.toggle("active");
        const icon = header.querySelector(".icon");

        if(item.classList.contains("active")){
            icon.textContent ="-";
        }
        else{
            icon.textContent="+";
        }
    });
});