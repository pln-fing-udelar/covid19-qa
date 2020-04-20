export default function Card({ title, description }) {
  return (
    <div class="border border-gray-300 text-gray-900 p-4 rounded-md">
      <h3 class="font-medium text-center text-lg mb-4">{title}</h3>
      {description}
    </div>
  );
}
