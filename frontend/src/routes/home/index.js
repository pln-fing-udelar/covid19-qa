import { Fragment } from "preact";
import Card from "../../components/card";
import faq from "../../data/faq.json";
import SearchInput from "../../components/searchInput";

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
          {faq.slice(0, 3).map((q) => (
            <div class="mb-4 md:mb-0 md:mr-4">
              <Card
                title={q.question}
                description={
                  <p>
                    {q.context.slice(0, q.answer_start_index)}
                    <b>
                      {q.context.slice(
                        q.answer_start_index,
                        q.answer_end_index
                      )}
                    </b>
                    {q.context.slice(q.answer_end_index, q.context.length)}
                  </p>
                }
              />
            </div>
          ))}
        </div>
      </section>
    </Fragment>
  );
};

export default Home;
