import Image from 'next/image';


const InfoCard = ({ imageSrc, children }: {
  imageSrc: string, children: React.ReactNode
}) => {

  return (
    <div className="flex flex-col items-center px-20">
      <Image
        src={imageSrc}
        width="60"
        height="60"
        alt="Loading..."></Image>
      <div className="flex flex-col items-center">
        {children}
      </div>
    </div>
  );
};

export default InfoCard;
