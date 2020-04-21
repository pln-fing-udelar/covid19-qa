import { Fragment } from "preact";
import FormattedAnswer from "../../components/formattedAnswer";

function SearchResult({ result }) {
  return (
    <Fragment>
      <h3 class="font-semibold text-lg mb-2">{result.title}</h3>
      <p>
        <FormattedAnswer
          answerStartIndex={result.answer_start_index}
          asnwerEndIndex={result.answer_end_index}
        >
          {result.context}
        </FormattedAnswer>
      </p>
      <span class="flex whitespace-pre-wrap items-center mt-2 text-gray-600 text-sm">
        <span>{`${result.date} / Fuente: `}</span>
        <a
          href={result.source.url}
          target="_blank"
          rel="noopener noreferrer"
          class="underline mr-1"
        >
          {result.source.name}
          <svg
            aria-hidden
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            class="h-4 w-4 fill-current inline ml-1"
          >
            <path d="M19 6.41L8.7 16.71a1 1 0 1 1-1.4-1.42L17.58 5H14a1 1 0 0 1 0-2h6a1 1 0 0 1 1 1v6a1 1 0 0 1-2 0V6.41zM17 14a1 1 0 0 1 2 0v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7c0-1.1.9-2 2-2h5a1 1 0 0 1 0 2H5v12h12v-5z" />
          </svg>
        </a>
      </span>
      <hr class="my-1" />
      <div class="flex items-center text-sm">
        <span class="mr-3">¿Te resultó útil?</span>
        <button name="Sí" title="Sí" class="p-1 hover:text-gray-600">
          <svg
            aria-hidden
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            class="h-4 w-4 fill-current"
          >
            <path d="M11 0h1v3l3 7v8a2 2 0 0 1-2 2H5c-1.1 0-2.31-.84-2.7-1.88L0 12v-2a2 2 0 0 1 2-2h7V2a2 2 0 0 1 2-2zm6 10h3v10h-3V10z" />
          </svg>
        </button>
        <button name="No" title="No" class="p-1 hover:text-gray-600">
          <svg
            aria-hidden
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            class="h-4 w-4 fill-current"
          >
            <path d="M11 20a2 2 0 0 1-2-2v-6H2a2 2 0 0 1-2-2V8l2.3-6.12A3.11 3.11 0 0 1 5 0h8a2 2 0 0 1 2 2v8l-3 7v3h-1zm6-10V0h3v10h-3z" />
          </svg>
        </button>
        <button
          name="Denunciar"
          title="Denunciar"
          class="p-1 hover:text-gray-600"
        >
          <svg
            aria-hidden
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            class="h-4 w-4 fill-current"
          >
            <path d="M7.667 12H2v8H0V0h12l.333 2H20l-3 6 3 6H8l-.333-2z" />
          </svg>
        </button>
      </div>
    </Fragment>
  );
}

export default SearchResult;
