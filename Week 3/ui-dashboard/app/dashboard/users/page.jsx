"use client";

import { useState } from "react";
import Badge from "@/components/ui/Badge";
import Modal from "@/components/ui/Modal";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

export default function UsersPage() {
  const [open, setOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  const users = [
    {
      name: "Esthera Jackson",
      email: "esthera@simmmple.com",
      role: "Manager",
      department: "Organization",
      status: "Online",
      avatar: "https://i.pravatar.cc/100?img=1",
      date: "14/06/21",
    },
    {
      name: "Alexa Liras",
      email: "alexa@simmmple.com",
      role: "Programmer",
      department: "Developer",
      status: "Offline",
      avatar: "https://i.pravatar.cc/100?img=3",
      date: "14/06/21",
    },
    {
      name: "Laurent Michael",
      email: "laurent@simmmple.com",
      role: "Executive",
      department: "Projects",
      status: "Online",
      avatar: "https://i.pravatar.cc/100?img=5",
      date: "14/06/21",
    },
    {
      name: "Freduardo Hill",
      email: "freduardo@simmmple.com",
      role: "Manager",
      department: "Organization",
      status: "Online",
      avatar: "https://i.pravatar.cc/100?img=10",
      date: "14/06/21",
    },
    {
      name: "Daniel Thomas",
      email: "daniel@simmmple.com",
      role: "Programmer",
      department: "Developer",
      status: "Offline",
      avatar: "https://i.pravatar.cc/100?img=33",
      date: "14/06/21",
    },
  ];

  const handleEdit = (user) => {
    setSelectedUser(user);
    setOpen(true);
  };

  return (
    <div className="p-6">
      <div className="bg-white rounded-2xl shadow-sm overflow-x-auto">
        <h2 className="px-6 py-4 text-lg font-semibold text-gray-800">
          Users Table
        </h2>

        <table className="w-full text-sm text-left">
          <thead className="text-gray-400 border-b">
            <tr>
              <th className="px-6 py-3">USER</th>
              <th className="px-6 py-3">FUNCTION</th>
              <th className="px-6 py-3">STATUS</th>
              <th className="px-6 py-3">EMPLOYED</th>
              <th className="px-6 py-3"></th>
            </tr>
          </thead>

          <tbody className="divide-y">
            {users.map((user, i) => (
              <tr key={i} className="hover:bg-gray-50 transition">
                {/* User */}
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <img
                      src={user.avatar}
                      alt={user.name}
                      className="w-10 h-10 rounded-full"
                    />
                    <div>
                      <p className="font-medium text-gray-800">{user.name}</p>
                      <p className="text-xs text-gray-500">{user.email}</p>
                    </div>
                  </div>
                </td>

                {/* Function */}
                <td className="px-6 py-4">
                  <p className="font-medium">{user.role}</p>
                  <p className="text-xs text-gray-500">{user.department}</p>
                </td>

                {/* Status */}
                <td className="px-6 py-4">
                  <Badge color={user.status === "Online" ? "green" : "gray"}>
                    {user.status}
                  </Badge>
                </td>

                {/* Date */}
                <td className="px-6 py-4 font-medium">{user.date}</td>

                {/* Edit */}
                <td
                  onClick={() => handleEdit(user)}
                  className="px-6 py-4 text-teal-600 font-medium cursor-pointer hover:underline"
                >
                  Edit
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Edit User"
      >
        {selectedUser && (
          <div className="space-y-4">
            <Input label="Name" defaultValue={selectedUser.name} />
            <Input label="Email" defaultValue={selectedUser.email} />
            <Input label="Role" defaultValue={selectedUser.role} />
            <Input label="Department" defaultValue={selectedUser.department} />

            <div className="flex gap-3 pt-4">
              <Button variant="secondary" onClick={() => setOpen(false)}>
                Cancel
              </Button>
              <Button>Save Changes</Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}