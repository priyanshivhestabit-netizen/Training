export default function ProfilePage() {
  return (
    <div className="w-full p-8 bg-gray-50 min-h-screen space-y-6">
      <h1 className="text-2xl font-bold">Profile</h1>

      {/* Card 1: Profile Summary */}
      <div className="w-full bg-white rounded-xl p-6 flex items-center gap-6 shadow-md">
        <div className="w-20 h-20 rounded-full bg-teal-100 flex items-center justify-center text-2xl font-bold text-teal-600">
          PV
        </div>

        <div>
          <h2 className="text-xl font-semibold">
            Priyanshi Verma
          </h2>
          <p className="text-gray-500">
            Admin
          </p>
          <p className="text-sm text-gray-400">
            India
          </p>
        </div>
      </div>

      {/* Card 2: Personal Information */}
      <div className="w-full bg-white rounded-xl p-6 shadow-md">

        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">
            Personal Information
          </h3>

          <button className="px-3 py-1 text-xs font-medium text-white bg-teal-500 border rounded hover:bg-teal-600">
            Edit
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
          <div>
            <p className="text-gray-400">First Name</p>
            <p className="font-medium">Priyanshi</p>
          </div>

          <div>
            <p className="text-gray-400">Last Name</p>
            <p className="font-medium">Verma</p>
          </div>

          <div>
            <p className="text-gray-400">Date of Birth</p>
            <p className="font-medium">13 Dec 2004</p>
          </div>

          <div>
            <p className="text-gray-400">Contact Number</p>
            <p className="font-medium">+91 98765 43210</p>
          </div>

          <div>
            <p className="text-gray-400">Email</p>
            <p className="font-medium">priyanshi@gmail.com</p>
          </div>

          <div>
            <p className="text-gray-400">User Role</p>
            <p className="font-medium">Admin</p>
          </div>
        </div>
      </div>

      {/* Card 3: Address */}
      <div className="w-full bg-white rounded-xl p-6 shadow-md">

        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">
            Address
          </h3>

          <button className="px-3 py-1 text-xs font-medium text-white bg-teal-500 rounded hover:bg-teal-600">
            Edit
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <p className="text-gray-400">Country</p>
            <p className="font-medium">India</p>
          </div>

          <div>
            <p className="text-gray-400">City</p>
            <p className="font-medium">Delhi</p>
          </div>

          <div>
            <p className="text-gray-400">Postal Code</p>
            <p className="font-medium">110001</p>
          </div>
        </div>
      </div>
    </div>
  );
}
