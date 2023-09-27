import Image from 'next/image';
import Link from 'next/link';
import RoundedButton from './components/RoundedButton';


export default function Home() {
  return (
    <>
      {
        /*
        <header>
          <nav>

          </nav>
        </header>
        */
      }
      <main className="flex flex-col">
        <div className="h-full w-full">
          <div className="flex flex-col">
            <section className="bg-cover bg-center bg-no-repeat min-h-screen bg-[url('/robot.png')] pt-10 px-40">
              <ul className="flex justify-between items-center">
                <li>
                  <Image
                    src="/logo1.png"
                    width="70"
                    height="53"
                    alt="Loading..."></Image>
                </li>
                <li className="text-stone-400 px-5">|</li>
                <li className="text-stone-500">
                  <Link href="/contacts">
                    <p>Контакти</p>
                  </Link>
                </li>
                <li className="grow"></li>
                <li className="text-stone-500">
                  <Link href="/register">
                    <p>Реєстрація</p>
                  </Link>
                </li>
                <li className="text-stone-400 px-5">|</li>
                <li className="text-stone-500">
                  <Link className="flex items-center" href="/login">
                    <p className="pr-2">Увійти</p>
                    <Image
                      src="/login.png"
                      width="20"
                      height="20"
                      alt="Loading..."></Image>
                  </Link>
                </li>
              </ul>
              <div className="font-medium text-7xl pb-10 pt-40">Matcher</div>
              <div className="pb-4">Набридло відслідковувати всі патерни самостійно?</div>
              <div className="font-medium text-2xl pb-10">
                <p>Довір це штучному інтелекту</p>
                <p>і насолоджуйся прибутком</p>
              </div>
              <div>
                <RoundedButton text="ПОЧАТИ" />
              </div>
            </section>
            <section className="flex flex-col items-center">
              <div>SOME TEXT</div>
              <div className="flex">
                <div>TEXT1</div>
                <div>TEXT2</div>
                <div>TEXT3</div>
              </div>
              <div className="flex">
                <div>TEXT1</div>
                <div>TEXT2</div>
              </div>
            </section>
            <section className="bg-yellow-500">Row 3</section>
            <section className="bg-red-500">Row 4</section>
            <section className="bg-indigo-500">Row 5</section>
            <section className="bg-purple-500">Row 6</section>
          </div>
        </div>
      </main>
      {
        /*
          <footer>
            <p>&copy; 2023 Your Website Name. All Rights Reserved.</p>
            <!-- You can include additional footer content or links here -->
          </footer>
        */
      }
    </>
  )
}
