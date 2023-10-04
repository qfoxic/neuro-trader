import Image from 'next/image';


const SubscriptionCardMenuItem = ({ bottomBorder, imageSrc, size, children }: {
  bottomBorder?: boolean, imageSrc: string, size: number, children: React.ReactNode
}) => {

  return (
    <div className={`flex align-center border-t p-2 ${bottomBorder && "border-b"}`}>
      <div className="flex align-center">
        <Image
          className="object-contain"
          src={imageSrc}
          width={size}
          height={size}
          alt="Loading..."></Image>
      </div>
      <div className="pl-2">{children}</div>
    </div>
  );
};

const StartEarnCard = ({ stepNumber, imageSrc, children }: {
  stepNumber: string, imageSrc: string, children: React.ReactNode
}) => {

  return (
    <div className="rounded rounded-tl-4xl bg-slate-300 px-4 py-3">
      <div className="flex justify-between">
        <div className="bg-blue-700 rounded-full p-2 ml-1 self-center">
          <Image
            className="object-contain"
            src={imageSrc}
            width={30}
            height={30}
            alt="...">
          </Image>
        </div>
        <p className="text-7xl text-white"><strong>{stepNumber}</strong></p>
      </div>
      {children}
    </div>
  );
};

export { StartEarnCard };
