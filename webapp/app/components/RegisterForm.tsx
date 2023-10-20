"use client"

import React, { useState, FormEvent } from 'react';
import Image from 'next/image';
import RoundedButton from './RoundedButton';
import { useRouter } from 'next/navigation';
import { toast } from 'react-toastify';

const RegisterForm = ({ }: {
}) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const router = useRouter();

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoading(true);

    try {
      const formData = new FormData(event.currentTarget);

      const response = await fetch('/api/register', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Не зареєстровано, повторіть спробу')
      }

      toast.success("Зареєстровано успішно");
      router.push("/");
    } catch (error: any) {
      toast.error(error.message);
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="bg-white" onSubmit={onSubmit}>
      <div className="flex items-center border rounded-lg mb-4 pl-4">
        <Image
          src="/name-icon.svg"
          width="18"
          height="18"
          alt="name-icon">
        </Image>
        <input required className="px-4 outline-none border-none py-3 w-full rounded-lg" type="text" name="name" placeholder="Імʼя" />
      </div>
      <div className="flex items-center border rounded-lg mb-4 pl-4">
        <Image
          src="/surname-icon.svg"
          width="18"
          height="18"
          alt="surname-icon">
        </Image>
        <input required className="px-4 outline-none border-none py-3 w-full rounded-lg" type="text" name="surname" placeholder="Прізвище" />
      </div>
      <div className="flex items-center border rounded-lg mb-4 pl-4">
        <Image
          src="/email-icon.svg"
          width="18"
          height="18"
          alt="email-icon">
        </Image>
        <input required className="px-4 outline-none border-none py-3 w-full rounded-lg" type="email" name="email" placeholder="Пошта" />
      </div>
      <div className="flex items-center border rounded-lg mb-4 pl-4">
        <Image
          src="/phone-icon.svg"
          width="18"
          height="18"
          alt="phone-icon">
        </Image>
        <input required className="px-4 outline-none border-none py-3 w-full rounded-lg" type="tel" name="phone" placeholder="Номер телефону" />
      </div>

      <div className="flex items-start mb-5">
        <div className="flex items-center h-5">
          <input id="terms" aria-describedby="terms" type="checkbox" required className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800" />
        </div>
        <div className="ml-3 text-sm">
          <label htmlFor="terms" className="text-gray-500">Я приймаю умови <a className="hover:underline text-blue-500" href="#">угоди користувача</a></label>
        </div>
      </div>
      <RoundedButton text="Зареєструватись" fullWidth="w-full" isLoading={isLoading} />
    </form>
  );
};

export default RegisterForm;
