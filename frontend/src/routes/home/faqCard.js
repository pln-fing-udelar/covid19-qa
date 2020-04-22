import FormattedAnswer from "../../components/formattedAnswer";
import FaqMetadata from "../../components/faqMetadata";

function FaqCard({ faq }) {
  return (
    <div class="mb-4 md:mb-0 md:mr-4 md:last:mr-0 border border-gray-300 rounded-md text-gray-900 p-4">
      <h3 class="font-medium text-center md:text-left text-lg mb-4">
        {faq.question}
      </h3>
      <FormattedAnswer
        answerStartIndex={faq.answer_start_index}
        asnwerEndIndex={faq.answer_end_index}
      >
        {faq.context}
      </FormattedAnswer>
      <FaqMetadata faq={faq} />
    </div>
  );
}

export default FaqCard;
