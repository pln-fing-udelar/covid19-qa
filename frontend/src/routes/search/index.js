import { Fragment } from "preact";
import SearchInput from "../../components/searchInput";
import SearchResult from "./searchResult";
import useAsync from "../../hooks/useAsync";
import { search } from "../../utils/api-client";
import SearchLoader from "./searchLoader";
import Layout from "../../components/layout";

export default function Search({ question }) {
  const { data: searchData, status } = useAsync(search, [question]);
  return (
    <Layout>
      <section class="md:max-w-xl mt-16 mb-10 flex">
        <SearchInput question={question} disableButton={status === "loading"} />
      </section>
      <section class="text-gray-800 min-w-lg">
        {status === "idle" || status === "loading" ? (
          <SearchLoader />
        ) : status === "error" ? (
          <p>
            Ocurrió un error mientras buscábamos una respuesta, intenta de nuevo
            más tarde.
          </p>
        ) : searchData.length > 0 ? (
          <Fragment>
            <h2 class="text-xl font-bold">Respuestas recomendadas</h2>
            <div class="border border-gray-700 p-3 rounded-md shadow mb-8">
              {searchData.slice(0, 3).map((result) => (
                <div class="mb-8 last:mb-0">
                  <SearchResult key={result.id} result={result} />
                </div>
              ))}
            </div>
            {searchData.slice(3).map((result) => (
              <div class="mb-8">
                <SearchResult result={result} />
              </div>
            ))}
          </Fragment>
        ) : (
          <p>
            No se encontraron respuestas, intenta de nuevo con otra pregunta.
          </p>
        )}
      </section>
    </Layout>
  );
}
