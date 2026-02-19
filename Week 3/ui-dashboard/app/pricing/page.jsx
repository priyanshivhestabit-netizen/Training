import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import LandingNavbar from "@/components/LandingNavbar";
const plans = [
  {
    name: "Free",
    price: "$0",
    description: "Perfect for getting started",
    features: [
      "Basic dashboard access",
      "Limited components",
      "Community support",
      "Single user",
    ],
    highlight: false,
  },
  {
    name: "Pro",
    price: "$19 / month",
    description: "Best for growing teams",
    features: [
      "Full dashboard access",
      "All UI components",
      "Priority support",
      "Up to 5 users",
    ],
    highlight: true,
  },
  {
    name: "Premium",
    price: "$49 / month",
    description: "For large scale products",
    features: [
      "Everything in Pro",
      "Unlimited users",
      "Advanced analytics",
      "Dedicated support",
    ],
    highlight: false,
  },
];

export default function PricingPage() {
  return (
    <>
    <LandingNavbar/>
    
    <main className="min-h-screen bg-white py-20 px-6">
      {/* Header */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold mb-4">
          Simple, transparent pricing
        </h1>
        <p className="text-gray-500 max-w-xl mx-auto">
          Choose the plan that fits your needs. Upgrade or downgrade anytime.
        </p>
      </div>

      {/* Pricing Cards */}
      <div className="max-w-6xl mx-auto grid gap-10 grid-cols-1 md:grid-cols-3">
        {plans.map((plan) => (
          <Card
            key={plan.name}
            className="
                        p-8 text-center
                        transition-all duration-300 ease-out
                        hover:scale-105
                        hover:shadow-2xl
                        hover:border-teal-400
                        border
                        cursor-pointer
                        "

          >
            <h2 className="text-xl font-semibold mb-2">
              {plan.name}
            </h2>

            <p className="text-gray-500 mb-6">
              {plan.description}
            </p>

            <div className="text-4xl font-bold text-teal-500 mb-6">
              {plan.price}
            </div>

            <ul className="text-sm text-gray-600 space-y-3 mb-8">
              {plan.features.map((feature) => (
                <li key={feature}>✔ {feature}</li>
              ))}
            </ul>

            <Button className="w-full">
              {plan.name === "Free"
                ? "Get Started"
                : "Upgrade Now"}
            </Button>
          </Card>
        ))}
      </div>
    </main>
    </>
  );
}
