import Link from "next/link";
import Button from "@/components/ui/Button";
import LandingNavbar from "@/components/LandingNavbar";
export default function LandingPage() {
  return (
    <>
    <main className="min-h-screen bg-white">
      
      {/* Top Navbar */}
      <LandingNavbar/>

      {/* Hero Section */}
      <section className="flex flex-col items-center text-center mt-32 px-6">
        <span className="mb-4 text-sm text-gray-500 border px-3 py-1 rounded-full">
          Top UI Platform
        </span>

        <h2 className="text-5xl font-bold max-w-3xl leading-tight">
          Clean dashboards for modern web apps
        </h2>

        <p className="text-gray-500 mt-6 max-w-xl">
          Build beautiful admin dashboards using reusable components
          and Next.js App Router.
        </p>

        <div className="mt-10 flex gap-4">
          <Link href="/signUp">
          <Button className="px-8">Get Started</Button>
          </Link>
        </div>
      </section>
    </main>
    </>
  );
}
