import FormattedAnswer from "../../components/formattedAnswer";

function FaqCard({ faq }) {
  return (
    <div class="mb-4 md:mb-0 md:mr-4 border border-gray-300 rounded-md text-gray-900 p-4">
      <h3 class="font-medium text-center text-lg mb-4">{faq.question}</h3>
      <FormattedAnswer
        answerStartIndex={faq.answer_start_index}
        asnwerEndIndex={faq.answer_end_index}
      >
        {faq.context}
      </FormattedAnswer>
      <span class="flex whitespace-pre-wrap items-center mt-2 text-gray-600 text-sm">
        <span>{`${faq.date} / Fuente: `}</span>
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
    </div>
  );
}

export default FaqCard;
