import "./globals.css";
import Sidebar from "../components/ui/Sidebar";
import Navbar from "../components/ui/Navbar";

export const metadata = {
  title: "Dashboard",
  description: "Dashboard Layout",
  icons:{
    icon:"/menu.png",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-700">
        <div className="flex">
          <Sidebar />

          <div className="flex-1 flex flex-col">
            <Navbar />
            <main className="flex-1 p-6 bg-gray-100 text-gray-900">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
