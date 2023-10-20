import Image from 'next/image';


const InfoCard = ({ imageSrc, children }: {
  imageSrc: string, children: React.ReactNode
}) => {

  return (
    <div className="flex flex-col items-center">
      <Image
        src={imageSrc}
        width="60"
        height="60"
        alt="Loading..."></Image>
      <div className="text-center mt-4 lg:mx-8">
        {children}
      </div>
    </div>
  );
};

export default InfoCard;
