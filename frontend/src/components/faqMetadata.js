export default function FaqMetadata({ faq }) {
  return (
    <span class="flex flex-col md:flex-row flex-wrap whitespace-pre-wrap text-gray-600 text-sm">
      <span>
        {faq.date}
        {` / `}
      </span>
      <span>
        Fuente:{" "}
        <a
          href={faq.source.url}
          target="_blank"
          rel="noopener noreferrer"
          class="underline mr-1"
        >
          {faq.source.name}
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
    </span>
  );
}
