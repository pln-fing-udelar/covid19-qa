import { useState } from "preact/hooks";
import { route } from "preact-router";

function SearchInput({ question, disableButton }) {
  const [query, setQuery] = useState(question || "");

  return (
    <form
      class="relative w-full"
      onSubmit={(e) => {
        e.preventDefault();
        route(`/search/${encodeURIComponent(query)}`);
      }}
    >
      <input
        aria-label="Haz una pregunta sobre COVID-19"
        name="question"
        type="text"
        required
        class="appearance-none rounded block w-full pl-4 pr-10 py-3 placeholder-gray-800 text-gray-900 outline-none focus:shadow-outline "
        placeholder="¿Dudas sobre COVID-19?"
        autoFocus
        value={query}
        onInput={(e) => setQuery(e.target.value)}
      />
      <button
        class="absolute inset-y-0 right-0 p-3 text-gray-600 flex items-center hover:bg-gray-400"
        type="submit"
        disabled={disableButton}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          class="w-6 h-6 fill-current"
        >
          <path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z" />
        </svg>
      </button>
    </form>
  );
}

export default SearchInput;
