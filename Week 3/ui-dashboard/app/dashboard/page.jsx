import Link from "next/link";
export default function DashboardPage() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { title: "Users", value: "1,245" },
          { title: "Revenue", value: "$23,400" },
          { title: "Orders", value: "320" },
          { title: "Pending", value: "12" },
        ].map((item, index) => (
          <div
            key={index}
            className="bg-white rounded-xl shadow-md p-5"
          >
            <p className="text-sm text-gray-500">{item.title}</p>
            <p className="text-2xl font-semibold mt-1">{item.value}</p>
          </div>
        ))}
      </div>

      {/* Overview Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Welcome Card */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold mb-2">Welcome back!!!</h2>
          <p className="text-gray-600">
            Here’s what’s happening with your dashboard today.
          </p>
          <Link href="/dashboard/profile">
          <button className="mt-4 text-sm text-teal-600 hover:text-teal-700 transition">
            View Profile 
          </button>
          </Link>
        </div>

        {/* Quick Info */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4">Quick Info</h2>
          <ul className="space-y-3 text-sm text-gray-600">
            <li>✔ New users signed up today: 24</li>
            <li>✔ Payments processed: 18</li>
            <li>✔ Server uptime: 99.98%</li>
          </ul>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>

        <ul className="space-y-4 text-sm">
          <li className="flex justify-between">
            <span>User John Doe signed up</span>
            <span className="text-gray-400">2h ago</span>
          </li>
          <li className="flex justify-between">
            <span>Payment received from Jane</span>
            <span className="text-gray-400">5h ago</span>
          </li>
          <li className="flex justify-between">
            <span>Profile updated</span>
            <span className="text-gray-400">1d ago</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
