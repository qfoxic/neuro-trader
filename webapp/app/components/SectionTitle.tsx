const SectionTitle = ({ children }: {
  children: React.ReactNode
}) => {

  return (
    <div className="flex flex-col items-center pb-16">
      {children}
    </div>
  );
};

export default SectionTitle;
