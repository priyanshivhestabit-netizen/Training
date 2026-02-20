import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import LandingNavbar from "@/components/LandingNavbar";

const features = [
  {
    title: "Communications",
    description:
      "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.",
    image: "/features/communication.png",
  },
  {
    title: "Inspired Design",
    description:
      "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.",
    image: "/features/design.png",
  },
  {
    title: "Happy Customers",
    description:
      "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.",
    image: "/features/customers.png",
  },
];

export default function FeaturesPage() {
  return (
    <>
    <LandingNavbar/>
    
    <main className="min-h-screen bg-teal-50 py-20 px-6">
      {/* Heading */}
      <div className="text-center mb-16">
        <p className="text-sm tracking-widest text-teal-600 uppercase mb-2">
          Features
        </p>
        <h1 className="text-4xl font-bold text-teal-700">
          Our Features & Services.
        </h1>
      </div>

      {/* Cards */}
      <div className="max-w-6xl mx-auto grid gap-10 grid-cols-1 md:grid-cols-3">
        {features.map((feature) => (
          <Card
            key={feature.title}
            className="flex flex-col items-center text-center p-8 transition-all duration-300 ease-out
                        hover:scale-105
                        hover:shadow-2xl
                        "
          >
            <img
              src={feature.image}
              alt={feature.title}
              className="w-32 h-32 object-contain mb-6"
            />

            <h3 className="text-lg font-semibold text-teal-700 mb-3">
              {feature.title}
            </h3>

            <p className="text-sm text-gray-500 mb-6">
              {feature.description}
            </p>

            <Button className="px-6 text-sm">MORE</Button>
          </Card>
        ))}
      </div>

    </main>
    </>
  );
}
