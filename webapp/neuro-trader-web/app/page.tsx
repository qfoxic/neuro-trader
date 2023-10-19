import Image from 'next/image';
import Link from 'next/link';
import RoundedButton from './components/RoundedButton';
import InfoCard from './components/InfoCard';
import SectionTitle from './components/SectionTitle';
import StrongBlue from './components/StrongBlue';
import StrongWhite from './components/StrongWhite';
import { SubscriptionCard, SubscriptionCardMenuItem } from './components/SubscriptionCard';
import { StartEarnCard } from './components/StartEarnCard';
import Modal from './components/Modal';
import RegisterForm from './components/RegisterForm';
import LoginForm from './components/LoginForm';

export interface ITab {
  title: string;
  children: React.ReactNode;
};

export default function Home({ searchParams }: any) {
  const showRegisterModal = searchParams?.showRegisterModal;
  const showLoginModal = searchParams?.showLoginModal;

  const tabs: ITab[] = [
    {
      title: "Вхід",
      children: <LoginForm />
    },
    {
      title: "Реєстрація",
      children: <RegisterForm />
    }
  ];

  return (
    <>
      {showRegisterModal && <Modal defaultTab={tabs[1]} tabs={tabs} />}
      {showLoginModal && <Modal defaultTab={tabs[0]} tabs={tabs} />}
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
            <section className="bg-cover bg-center min-h-screen min-w-screen bg-[url('/robot.png')] p-10 md:px-40">
              <ul className="flex justify-between items-center">
                <li>
                  <Image
                    src="/logo1.png"
                    width="70"
                    height="53"
                    className="w-10 md:w-[70px]"
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
                  <Link className="flex items-center" href="/?showLoginModal=true">
                    <p className="pr-2">Увійти</p>
                    <Image
                      src="/login.png"
                      width="20"
                      height="20"
                      alt="Loading..."></Image>
                  </Link>
                </li>
              </ul>
              <div className="font-medium text-5xl md:text-7xl pb-8 md:pb-10 pt-40">Matcher</div>
              <div className="pb-4">Набридло відслідковувати всі патерни самостійно?</div>
              <div className="font-medium text-1xl md:text-2xl pb-10">
                <p>Довір це штучному інтелекту</p>
                <p>і насолоджуйся прибутком</p>
              </div>
              <Link href="/?showRegisterModal=true">
                <RoundedButton text="ПОЧАТИ" />
              </Link>
            </section>
            <section className="px-10 py-12 md:p-24 container mx-auto lg:px-40 xl:px-48">
              <SectionTitle>
                <p className="font-medium text-2xl pb-4">Заробляйте разом з роботом <StrongBlue>Matcher</StrongBlue></p>
                <p><StrongBlue>Matcher</StrongBlue> налаштовують професіонали під вас і ваші потреби</p>
                <p>Він моніторить ринок <StrongBlue>24/5</StrongBlue> у пошуках патернів для прибутку на вашому рахунку</p>
              </SectionTitle>
              <div className="flex flex-wrap justify-center">
                <div className="w-[50%] md:w-[33%] p-4 ">
                  <InfoCard imageSrc="/percentage.png">
                    Річний прибуток від <StrongBlue>60%</StrongBlue> до <StrongBlue>100%</StrongBlue>
                  </InfoCard>
                </div>
                <div className="w-[50%] md:w-[33%] p-4 ">
                  <InfoCard imageSrc="/neural-network.png">
                    Алгоритм налаштований <StrongBlue>на всі випадки</StrongBlue> на ринку
                  </InfoCard>
                </div>
                <div className="w-[50%] md:w-[33%] p-4 ">
                  <InfoCard imageSrc="/remote-access.png">
                    Робот може працювати як на вашому <StrongBlue>компʼютері</StrongBlue> так і <StrongBlue>віддалено</StrongBlue>
                  </InfoCard>
                </div>
                <div className="w-[50%] md:w-[33%] p-4 ">
                  <InfoCard imageSrc="/free.png">
                    <StrongBlue>Безкоштовний</StrongBlue> тестовий період
                  </InfoCard>
                </div>
                <div className="w-[100%] md:w-[33%] p-4 ">
                  <InfoCard imageSrc="/number.png">
                    Працює на <StrongBlue>5</StrongBlue> валютних парах
                  </InfoCard>
                </div>
              </div>
            </section>
            <section className="bg-sky-200 flex flex-col items-center px-10 py-12 md:p-24">
              <SectionTitle>
                <p className="font-medium text-2xl pb-2 md:pb-4">Переваги робота <StrongBlue>Matcher</StrongBlue></p>
              </SectionTitle>
              <div className="flex flex-col pb-8 gap-16 md:gap-24">
                <InfoCard imageSrc="/trading.png">
                  <h1 className="pb-3 pt-1 font-bold">Штучний інтелект</h1>
                  <p><StrongBlue>Matcher</StrongBlue> відслідковує кожне коливання ринку</p>
                  <p>точно і швидко відкриває позицію, як тільки знаходить патерн</p>
                  <p>Робот працює <StrongBlue>24/5</StrongBlue>, тому відслідковує всі рухи ринку</p>
                  <p>і максимізує прибутки</p>
                </InfoCard>
                <InfoCard imageSrc="/rules.png">
                  <h1 className="pb-3 pt-1 font-bold">Торгівля за правилами</h1>
                  <p><StrongBlue>Matcher</StrongBlue> має чіткі правила мані-менеджменту і ризик-менеджменту</p>
                  <p>для мінімізації ризиків і торгівлі по правилах</p>
                </InfoCard>
                <InfoCard imageSrc="/blur.png">
                  <h1 className="pb-3 pt-1 font-bold">Прибуткові патерни</h1>
                  <p><StrongBlue>Matcher</StrongBlue> поєднує в собі сотні патернів</p>
                  <p>які мають <StrongBlue>дохідність вище 70%</StrongBlue></p>
                </InfoCard>
              </div>
            </section>
            <section className="flex flex-col items-center px-10 py-12 md:p-24">
              <SectionTitle>
                <p className="font-medium text-2xl pb-2 md:pb-4">Вартість робота <StrongBlue>Matcher</StrongBlue></p>
              </SectionTitle>
              <div className="flex flex-col min-[450px]:flex-row gap-6">
                <SubscriptionCard
                  main={false}
                  header={"Тестовий період"}
                  footer={<><p><StrongBlue>0%</StrongBlue></p><p>з доходу за місяць</p></>}
                >
                  <SubscriptionCardMenuItem imageSrc="/check.png" size={12}>
                    <p>Період дії <StrongBlue>1 місяць</StrongBlue></p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem imageSrc="/close.png" size={9} disabled>
                    <p>Можливість налаштувати</p>
                    <p>робота самостійно або</p>
                    <p>з експертом</p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem imageSrc="/close.png" size={9} disabled>
                    <p>Супровід і підтримка</p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem bottomBorder={true} imageSrc="/close.png" size={9} disabled>
                    <p>Абонентська плата</p>
                  </SubscriptionCardMenuItem>
                </SubscriptionCard>
                <SubscriptionCard
                  header={"Платна підписка"}
                  footer={<><p><StrongBlue>20%</StrongBlue></p><p>з доходу за місяць</p></>}
                >
                  <SubscriptionCardMenuItem imageSrc="/check.png" size={12}>
                    <p>Період дії <StrongBlue>1 місяць</StrongBlue></p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem imageSrc="/check.png" size={12}>
                    <p>Можливість налаштувати</p>
                    <p>робота <StrongBlue>самостійно</StrongBlue> або</p>
                    <p>з <StrongBlue>експертом</StrongBlue></p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem imageSrc="/check.png" size={12}>
                    <p><StrongBlue>Супровід</StrongBlue> і <StrongBlue>підтримка</StrongBlue></p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem bottomBorder={true} imageSrc="/check.png" size={12}>
                    <p>Абонентська плата</p>
                  </SubscriptionCardMenuItem>
                </SubscriptionCard>
              </div>
              <div className="flex flex-col">
                <div className="flex flex-col items-center py-10">
                  <RoundedButton
                    buttonColor={"bg-white"}
                    textColor={"text-gray-400"}
                    border="border-2"
                    text="Детальний опис робота"
                    icon="/download.png" />
                </div>
              </div>
            </section>
            <section className="bg-blue-950 items-center px-10 py-12 md:p-24">
              <div className="container mx-auto lg:px-30 xl:px-44">
                <SectionTitle>
                  <p className="font-medium text-2xl"><StrongWhite>Щоб почати заробляти разом з Matcher</StrongWhite></p>
                  <p className="font-medium text-xl text-white">потрібно здійснити декілька простих кроків</p>
                </SectionTitle>
                <div className="flex justify-center flex-wrap">
                  <StartEarnCard stepNumber="1." imageSrc="/pen.png">
                    <span className="font-bold">Пройти реєстрацію</span> і дочекатись появи токену
                  </StartEarnCard>
                  <StartEarnCard stepNumber="2." imageSrc="/deal.png">
                    <div>
                      <span className="font-bold">Відкрити</span> і поповнити <span className="font-bold">рахунок</span> в <span className="font-bold">брокера</span>
                    </div>
                    <div className="flex">
                      <p className="flex flex-col text-sky-700">
                        <span>вибирай надійних і перевірених брокерів</span>
                        <Link className="font-bold" href="https://my.esperio.org/agent_pp.html?agent_pp=27177553">esperio.org</Link>
                        <Link className="font-bold" href="https://my.teletrade-dj.com/agent_pp.html?agent_pp=24877377">teletrade.com.ua</Link>
                      </p>

                    </div>
                  </StartEarnCard>
                  <StartEarnCard stepNumber="3." imageSrc="/development.png">
                    <span className="font-bold">Скачати і встановити</span> робота по інструкції в текстовому документі, який буде з роботом
                  </StartEarnCard>
                </div>
              </div>
            </section>
            <section className="flex-col items-center px-10 py-12 md:p-24">
              <SectionTitle>
                <p className="font-medium text-2xl"><span className="font-bold">Ми на зв`язку</span></p>
              </SectionTitle>
              <div className="flex justify-center gap-4">
                <div>EMAIL</div>
                <div>telegram</div>
              </div>
            </section>
          </div>
        </div>
      </main>
      <footer className="bg-blue-950 flex flex-col items-center px-10 py-12 md:p-24">
        <Image
          src="/logo2.svg"
          width="55"
          height="20"
          className="w-55 md:w-[80px] mb-4"
          alt="Matcher footer logo">
        </Image>
        <Image
          src="/title.svg"
          width="100"
          height="20"
          className="w-100 md:w-[147px]"
          alt="Matcher footer title">
        </Image>
      </footer>
    </>
  )
}
