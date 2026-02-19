import Link from "next/link";
import Button from "./Button";
export default function Navbar() {
  return (
    <header className="h-16 bg-white border-b shadow-sm flex items-center justify-between px-6">
      <div>
        <h2 className="text-lg font-semibold">Pages</h2>
      </div>

      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="Type here..."
          className="border rounded-lg px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <Link href="/signIn">
        <Button className="px-6">Sign In</Button>
        </Link>
      </div>
    </header>
  );
}
