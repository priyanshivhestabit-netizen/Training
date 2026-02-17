export default function Navbar() {
  return (
    <header className="bg-white p-4 shadow-sm flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-900">Pages / Tables</p>
        <h2 className="text-lg text-gray-900 font-semibold">Tables</h2>
      </div>

      <div className="flex items-center gap-4">
        <input
            type="text"
            placeholder="Type here..."
            className="bg-gray-50 text-gray-800 placeholder:text-gray-400 
                      border border-gray-300 
                      rounded-xl px-4 py-2 text-sm
                      focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500
                      transition"
        />


        <button className="text-sm font-medium text-gray-600">
          Sign In
        </button>
      </div>
    </header>
  );
}
