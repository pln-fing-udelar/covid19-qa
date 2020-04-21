import { Fragment } from "preact";
import faqData from "../../data/faq.json";
import SearchInput from "../../components/searchInput";
import FaqCard from "./faqCard";
const Home = () => {
  return (
    <Fragment>
      <section class="mx-6 sm:mx-8 md:mx-auto md:max-w-xl mt-16 mb-10 flex">
        <SearchInput />
      </section>
      <section class="mx-auto">
        <h2 class="text-2xl font-semibold text-center text-gray-900 mb-4">
          Preguntas frecuentes
        </h2>
        <div class="flex flex-col md:flex-row">
          {faqData.slice(0, 3).map((faq) => (
            <FaqCard faq={faq} />
          ))}
        </div>
      </section>
    </Fragment>
  );
};

export default Home;