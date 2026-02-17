export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-white border-r px-6 py-8">
      <h1 className="text-xl font-bold tracking-wide mb-10 text-gray-800">
  DASHBOARD
</h1>


      <nav className="space-y-3">
        <a className="flex items-center gap-3 p-3 rounded-xl bg-gray-100 text-gray-400 font-medium">
          Dashboard
        </a>

        <a className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-100 text-gray-600">
          Tables
        </a>

        <a className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-100 text-gray-600">
          Billing
        </a>

        <a className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-100 text-gray-600">
          RTL
        </a>

        <div className="pt-6 text-xs uppercase text-gray-400 tracking-wider">
          Account Pages
        </div>

        <a className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-100 text-gray-600">
          Profile
        </a>

        <a className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-100 text-gray-600">
          Sign In
        </a>

        <a className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-100 text-gray-600">
          Sign Up
        </a>
      </nav>
    </aside>
  );
}
