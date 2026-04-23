export default function Card({ title, children, className = "" }) {
  return (
    <div className={`bg-white rounded-xl shadow-sm p-8 w-full max-w-md ${className}`}>
      {title && (
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
      )}
      {children}
    </div>
  );
}
