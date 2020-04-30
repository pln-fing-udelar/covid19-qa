import faqData from "../../data/faq.json";
import SearchInput from "../../components/searchInput";
import FaqCard from "./faqCard";
import FaqHeader from "../../components/faqHeader";
import HomeLayout from "../../components/homeLayout";
import { route } from "preact-router";

const Home = () => {
  return (
    <HomeLayout>
      <section class="mx-6 sm:mx-8 md:mx-auto md:max-w-xl mb-10 flex">
        <SearchInput
          onSubmit={(query) => {
            route(`/search/${encodeURIComponent(query)}`);
          }}
        />
      </section>
      <section class="mx-auto flex flex-col">
        <div class="flex justify-between items-center mb-4">
          <FaqHeader />
          <a href="/faq" class="underline text-gray-900">
            Ver más
          </a>
        </div>
        <div class="flex flex-col md:flex-row mt-2">
          {faqData.slice(0, 3).map((faq) => (
            <FaqCard faq={faq} />
          ))}
        </div>
      </section>
    </HomeLayout>
  );
};

export default Home;
