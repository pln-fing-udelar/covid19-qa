function HomeLayout({ children }) {
  return (
    <main class="px-4 sm:px-8 md:px-16 lg:px-32 max-w-6xl bg-gray-300 shadow rounded-md py-8 m-4 md:m-8">
      {children}
    </main>
  );
}

export default HomeLayout;
