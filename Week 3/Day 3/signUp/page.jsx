import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Link from "next/link";
import LandingNavbar from "@/components/LandingNavbar";

export default function SignUpPage() {
  return (
    <>
    <LandingNavbar/>
    <main className="min-h-screen flex items-center justify-center bg-white px-4">
      <Card className="w-full max-w-md">
        <h1 className="text-2xl font-bold text-teal-500 mb-2">
          Create an account
        </h1>

        <p className="text-gray-500 mb-6">
          Enter your details to create your account
        </p>

        <div className="flex flex-col gap-4">
          <Input
            label="Full Name"
            placeholder="Your full name"
          />

          <Input
            label="Email"
            placeholder="Your email address"
          />

          <Input
            label="Password"
            type="password"
            placeholder="Create a password"
          />

          <Input
            label="Confirm Password"
            type="password"
            placeholder="Confirm your password"
          />

          <div className="flex items-start gap-2 text-sm text-gray-600">
            <input type="checkbox" className="mt-1" />
            <span>
              I agree to the{" "}
              <span className="text-teal-500 cursor-pointer">
                Terms & Conditions
              </span>
            </span>
          </div>
            <Link href="/signIn">
          <Button>SIGN UP</Button>
            </Link>
          <p className="text-sm text-center text-gray-500">
            Already have an account?{" "}
            <Link href="/signIn" className="text-teal-500">
              Sign in
            </Link>
          </p>
        </div>
      </Card>
    </main>
    </>
  );
}
