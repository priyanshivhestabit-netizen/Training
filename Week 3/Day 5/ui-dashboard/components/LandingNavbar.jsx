import Link from "next/link";
import Button from "@/components/ui/Button";

export default function LandingNavbar() {
  return (
    <header className="flex items-center justify-between px-10 py-6">
        <h1 className="font-bold text-xl">Purity UI</h1>

        <nav className="flex items-center gap-8 text-sm">
          <Link href="/">Home</Link>
          <Link href="/features">Features</Link>
          <Link href="/about">About</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/signIn">
            <Button className="px-6">Login</Button>
          </Link>
        </nav>
      </header>
  );
}
