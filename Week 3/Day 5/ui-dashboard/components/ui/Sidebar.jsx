export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-gray-50 border-r shadow-sm p-6">
      <h1 className="text-xl font-bold mb-8">PURITY UI DASHBOARD</h1>

      <nav className="space-y-4">
        <a href="/" className="block p-2 rounded-lg hover:bg-gray-100">
          Homepage
        </a>
        <a href="/dashboard" className="block p-2 rounded-lg hover:bg-gray-100">
          Dashboard
        </a>
        <a href="/dashboard/users" className="block p-2 rounded-lg hover:bg-gray-100">
          Users
        </a>
        <a href="/dashboard/billing" className="block p-2 rounded-lg hover:bg-gray-100">
          Billing
        </a>

        <div className="pt-6 text-gray-400 text-sm uppercase">
          Account Pages
        </div>

        <a href="/dashboard/profile" className="block p-2 rounded-lg hover:bg-gray-100">
          Profile
        </a>
        <a href="/signIn" className="block p-2 rounded-lg hover:bg-gray-100">
          Sign In
        </a>
        <a href="/signUp" className="block p-2 rounded-lg hover:bg-gray-100">
          Sign Up
        </a>
      </nav>
    </aside>
  );
}
