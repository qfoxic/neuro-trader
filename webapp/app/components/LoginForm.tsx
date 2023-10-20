import Image from 'next/image';
import RoundedButton from './RoundedButton';


const LoginForm = ({ }: {
}) => {

  return (
    <form className="bg-white">
      <div className="flex items-center border rounded-lg mb-4 pl-4">
        <Image
          src="/email-icon.svg"
          width="18"
          height="18"
          alt="email-icon">
        </Image>
        <input required className="px-4 outline-none border-none py-3 w-full rounded-lg" type="email" name="" id="" placeholder="Пошта" />
      </div>
      <div className="flex items-center border rounded-lg mb-5 pl-4">
        <Image
          src="/password-icon.svg"
          width="18"
          height="18"
          alt="password-icon">
        </Image>
        <input required className="px-4 outline-none border-none py-3 w-full rounded-lg" type="password" name="" id="" placeholder="Пароль" />
      </div>
      <RoundedButton text="Увійти" fullWidth="w-full" />
    </form>
  );
};

export default LoginForm;
