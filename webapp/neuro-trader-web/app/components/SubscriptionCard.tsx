import Image from 'next/image';
import RoundedButton from './RoundedButton';


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

const SubscriptionCard = ({ main=true, header, footer, children }: {
  main?: boolean, header: React.ReactNode, footer: React.ReactNode, children: React.ReactNode
}) => {

  return (
    <div className="border-2 rounded-xl flex flex-col items-center p-5">
      <strong className="font-medium pb-4">{header}</strong>
      <div className="flex flex-col items-left pb-2">
        {children}
      </div>
      <div className="flex flex-col items-center pb-2">
        {footer}
      </div>
      <div className="flex flex-col items-center">
        <RoundedButton buttonColor={main ? "bg-blue-500": "bg-gray-200"} textColor={main ? "text-white": "text-sky-700"} text="ОБРАТИ" />
      </div>
    </div>
  );
};

export { SubscriptionCard, SubscriptionCardMenuItem };
