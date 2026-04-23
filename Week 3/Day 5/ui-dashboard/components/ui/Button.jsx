export default function Button({
  children,
  className="",
  ...props})
  {

  return (
    <button
      className={`w-full rounded-lg font-medium transition bg-teal-500 text-white hover:bg-teal-600 px-4 py-2 text-sm ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
