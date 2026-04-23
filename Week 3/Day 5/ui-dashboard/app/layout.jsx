import "./globals.css";

export const metadata = {
  title: "Purity UI Dashboard",
  description: "Next.js App Router Practice",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-900">
        {children}
      </body>
    </html>
  );
}
