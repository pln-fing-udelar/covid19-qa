import { Fragment } from "preact";
import SearchInput from "../../components/searchInput";
import SearchResult from "./searchResult";
import searchData from "../../data/search.json";

export default function Search({ question }) {
  return (
    <Fragment>
      <section class="md:max-w-xl mt-16 mb-10 flex">
        <SearchInput question={question} />
      </section>
      <section class="text-gray-800">
        <h2 class="text-xl font-bold">Respuestas recomendadas</h2>
        <div class="border border-gray-700 p-3 rounded-md shadow mb-8">
          {searchData.slice(0, 3).map((result) => (
            <div class="mb-8 last:mb-0">
              <SearchResult result={result} />
            </div>
          ))}
        </div>
        {searchData.slice(3).map((result) => (
          <div class="mb-8">
            <SearchResult result={result} />
          </div>
        ))}
      </section>
    </Fragment>
  );
}
