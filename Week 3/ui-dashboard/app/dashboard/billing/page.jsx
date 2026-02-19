export default function BillingPage() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Billing</h1>

      {/* Current Plan */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold mb-2">Current Plan</h2>
        <p className="text-gray-600 mb-4">
          You are currently on the <span className="font-medium">Pro Plan</span>
        </p>
        <p className="text-3xl font-bold text-teal-600">$29/month</p>
      </div>

      {/* Payment Method */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">Payment Method</h2>

        <div className="flex justify-between items-center">
          <div>
            <p className="font-medium">Visa ending in 4242</p>
            <p className="text-sm text-gray-500">Expires 08/26</p>
          </div>

          <button className="text-sm text-teal-600 hover:text-teal-500 transition">
            Update
          </button>
        </div>
      </div>

      {/* Billing History */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">Billing History</h2>

        <ul className="space-y-3 text-sm">
          <li className="flex justify-between">
            <span>Jan 2026</span>
            <span className="font-medium">$29</span>
          </li>
          <li className="flex justify-between">
            <span>Dec 2025</span>
            <span className="font-medium">$29</span>
          </li>
          <li className="flex justify-between">
            <span>Nov 2025</span>
            <span className="font-medium">$29</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
