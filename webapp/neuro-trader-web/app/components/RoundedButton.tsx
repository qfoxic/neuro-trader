"use client"

import { useState } from "react";


const RoundedButton = ({ text, buttonColor="bg-blue-500", textColor="text-white" }: { text: string, buttonColor?: string, textColor?: string }) => {
  const [clicked, setClicked] = useState(false);

  const handleClick = () => {
  };

  return (
    <button
      type="submit"
      className={`px-12 py-2 ${buttonColor} ${textColor} rounded-full hover:ring-2`}
      onClick={handleClick}
    >
      {text}
    </button>
  );
};

export default RoundedButton;
