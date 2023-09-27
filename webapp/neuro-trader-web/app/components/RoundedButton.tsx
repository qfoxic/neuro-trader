"use client"

import { useState } from 'react';

const RoundedButton = ({ text }: { text: string }) => {
  const [clicked, setClicked] = useState(false);

  const handleClick = () => {
  };

  return (
    <button
      type="submit"
      className="px-12 py-2 bg-blue-500 text-white rounded-full focus:outline-none focus:ring-2 focus:ring-opacity-50"
      onClick={handleClick}
    >
      {text}
    </button>
  );
};

export default RoundedButton;
