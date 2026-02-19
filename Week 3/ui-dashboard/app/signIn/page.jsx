import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Link from "next/link";
import LandingNavbar from "@/components/LandingNavbar";

export default function HomePage() {
  return (
    <>
    <LandingNavbar/>
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card>
        <h1 className="text-2xl font-bold text-teal-400 mb-2">
          Welcome Back
        </h1>
        <p className="text-gray-500 mb-6">
          Enter your email and password to sign in
        </p>

        <div className="flex flex-col gap-4">
          <Input label="Email" placeholder="Your email address"/>
          <Input label="Password" type="password" placeholder="Your password"/>

          <div className="flex items-center gap-2 text-sm text-gray-600">
            <input type="checkbox" />
            Remember me
          </div>
        <Link href="/dashboard">
          <Button>SIGN IN</Button>
          </Link>

          <p className="text-sm text-center text-gray-500">
            Don&apos;t have an account?{" "}
            <Link href="/signUp">
            <span className="text-teal-400 cursor-pointer">Sign up</span>
            </Link>
          </p>
        </div>
      </Card>
    </main>
    </>
  );
}
