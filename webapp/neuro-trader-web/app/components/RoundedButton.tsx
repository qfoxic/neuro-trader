"use client"

import { useState } from "react";
import Image from 'next/image';


const RoundedButton = ({ text, buttonColor="bg-blue-500", textColor="text-white", border, icon }:
        { text: string, buttonColor?: string, textColor?: string, border?: string, icon?: string }) => {
  const [clicked, setClicked] = useState(false);

  const handleClick = () => {
  };

  return (
    <button
      type="submit"
      className={`flex items-center gap-3 px-12 py-2 ${buttonColor} ${textColor} ${border} rounded-full hover:ring-2`}
      onClick={handleClick}
    >
      {
        icon ? <Image className="object-contain" src={icon} width={16} height={16} alt="..." /> : ""
      }
      <p>{text}</p>
    </button>
  );
};

export default RoundedButton;
