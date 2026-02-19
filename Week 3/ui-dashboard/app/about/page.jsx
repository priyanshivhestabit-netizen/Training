import Card from "@/components/ui/Card";
import LandingNavbar from "@/components/LandingNavbar";
export default function AboutPage() {
  return (
    <>
    <LandingNavbar/>
    <main className="min-h-screen bg-white py-20 px-6">
      {/* Header */}
      <section className="max-w-4xl mx-auto text-center mb-20">
        <h1 className="text-4xl font-bold mb-6">
          About Purity UI
        </h1>
        <p className="text-gray-500 text-lg">
          Purity UI is a modern dashboard system built to help developers
          create clean, scalable, and user-friendly web applications faster.
        </p>
      </section>

      {/* Mission + Vision */}
      <section className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 mb-20">
        <Card className="p-8">
          <h2 className="text-2xl font-semibold mb-4 text-teal-500">
            Our Mission
          </h2>
          <p className="text-gray-600 leading-relaxed">
            Our mission is to simplify dashboard development by providing
            reusable UI components, clean layouts, and scalable architecture
            using Next.js and modern frontend best practices.
          </p>
        </Card>

        <Card className="p-8">
          <h2 className="text-2xl font-semibold mb-4 text-teal-500">
            Our Vision
          </h2>
          <p className="text-gray-600 leading-relaxed">
            We envision a world where developers can focus on building
            meaningful products instead of reinventing common UI patterns.
            Purity UI aims to become the go-to dashboard foundation for modern apps.
          </p>
        </Card>
      </section>

      {/* Values */}
      <section className="max-w-6xl mx-auto mb-20">
        <h2 className="text-3xl font-bold text-center mb-12">
          Our Core Values
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {[
            {
              title: "Clarity",
              text: "We believe in simple, clean interfaces that are easy to understand and use.",
            },
            {
              title: "Consistency",
              text: "Reusable components and predictable layouts help teams move faster.",
            },
            {
              title: "Performance",
              text: "Optimized UI and smart architecture ensure fast, reliable applications.",
            },
          ].map((value) => (
            <Card key={value.title} className="p-8 text-center">
              <h3 className="text-xl font-semibold text-teal-500 mb-3">
                {value.title}
              </h3>
              <p className="text-gray-600">
                {value.text}
              </p>
            </Card>
          ))}
        </div>
      </section>

     
    </main>
    </>
  );
}
