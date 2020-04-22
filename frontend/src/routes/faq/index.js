import { Fragment } from "preact";
import faq from "../../data/faq.json";
import FaqHeader from "../../components/faqHeader";
import FormattedAnswer from "../../components/formattedAnswer";
import FaqMetadata from "../../components/faqMetadata";

export default function Faq() {
  return (
    <Fragment>
      <section class="text-gray-800 mt-8">
        <div class="mb-4">
          <FaqHeader />
        </div>
        {faq.map((q) => (
          <div class="mb-8">
            <h3 class="font-semibold text-lg mb-2">{q.question}</h3>
            <p>
              <FormattedAnswer
                answerStartIndex={q.answer_start_index}
                asnwerEndIndex={q.answer_end_index}
              >
                {q.context}
              </FormattedAnswer>
            </p>
            <hr class="my-1" />
            <FaqMetadata faq={q} />
          </div>
        ))}
      </section>
    </Fragment>
  );
}
