import { Fragment } from "preact";
import FormattedAnswer from "../../components/formattedAnswer";
import SearchResultMetadata from "./searchResultMetadata";
import FeedbackSection from "./feedbackSection";
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
      <SearchResultMetadata result={result} />
      <hr class="my-1" />
      <div class="flex items-center text-sm">
        <FeedbackSection answerId={result.id} />
      </div>
    </Fragment>
  );
}

export default SearchResult;
