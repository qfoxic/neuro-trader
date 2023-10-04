import Image from 'next/image';
import Link from 'next/link';
import RoundedButton from './components/RoundedButton';
import InfoCard from './components/InfoCard';
import SectionTitle from './components/SectionTitle';
import StrongBlue from './components/StrongBlue';
import StrongWhite from './components/StrongWhite';
import { SubscriptionCard, SubscriptionCardMenuItem } from './components/SubscriptionCard';
import { StartEarnCard } from './components/StartEarnCard';


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
            <section className="bg-cover bg-center min-h-screen bg-[url('/robot.png')] py-10 px-40">
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
            <section className="flex flex-col items-center py-20">
              <SectionTitle>
                <p className="font-medium text-2xl pb-4">Заробляйте разом з роботом <StrongBlue>Matcher</StrongBlue></p>
                <p><StrongBlue>Matcher</StrongBlue> налаштовують професіонали під вас і ваші потреби</p>
                <p>Він моніторить ринок <StrongBlue>24/5</StrongBlue> у пошуках патернів для прибутку на вашому рахунку</p>
              </SectionTitle>
              <div className="flex pb-16">
                <InfoCard imageSrc="/percentage.png">
                  <p>Річний прибуток</p>
                  <p>від <StrongBlue>60%</StrongBlue> до <StrongBlue>100%</StrongBlue></p>
                </InfoCard>
                <InfoCard imageSrc="/neural-network.png">
                  <p>Алгоритм налаштований</p>
                  <p><StrongBlue>на всі випадки</StrongBlue> на ринку</p>
                </InfoCard>
                <InfoCard imageSrc="/remote-access.png">
                  <p>Робот може працювати</p>
                  <p>як на вашому <StrongBlue>компʼютері</StrongBlue></p>
                  <p>так і <StrongBlue>віддалено</StrongBlue></p>
                </InfoCard>
              </div>
              <div className="flex">
                <InfoCard imageSrc="/free.png">
                  <p><StrongBlue>Безкоштовний</StrongBlue></p>
                  <p>тестовий період</p>
                </InfoCard>
                <InfoCard imageSrc="/number.png">
                  <p>Працює на <StrongBlue>5</StrongBlue>5 валютних</p>
                  <p>парах</p>
                </InfoCard>
              </div>
            </section>
            <section className="bg-sky-200 flex flex-col items-center py-20">
              <SectionTitle>
                <p className="font-medium text-2xl pb-4">Переваги робота <StrongBlue>Matcher</StrongBlue></p>
              </SectionTitle>
              <div className="flex flex-col pb-16 gap-28">
                <InfoCard imageSrc="/trading.png">
                  <h1 className="py-3"><strong>Штучний інтелект</strong></h1>
                  <p><StrongBlue>Matcher</StrongBlue> відслідковує кожне коливання ринку</p>
                  <p>точно і швидко відкриває позицію, як тільки знаходить патерн</p>
                  <p>Робот працює <StrongBlue>24/5</StrongBlue>, тому відслідковує всі рухи ринку</p>
                  <p>і максимізує прибутки</p>
                </InfoCard>
                <InfoCard imageSrc="/rules.png">
                  <h1 className="py-3"><strong>Торгівля за правилами</strong></h1>
                  <p><StrongBlue>Matcher</StrongBlue> має чіткі правила мані-менеджменту і ризик-менеджменту</p>
                  <p>для мінімізації ризиків і торгівлі по правилах</p>
                </InfoCard>
                <InfoCard imageSrc="/blur.png">
                  <h1 className="py-3"><strong>Прибуткові патерни</strong></h1>
                  <p><StrongBlue>Matcher</StrongBlue>поєднує в собі сотні патернів</p>
                  <p>які мають <StrongBlue>дохідність вище 70%</StrongBlue></p>
                </InfoCard>
              </div>
            </section>
            <section className="flex flex-col items-center py-20">
              <SectionTitle>
                <p className="font-medium text-2xl pb-4">Вартість робота <StrongBlue>Matcher</StrongBlue></p>
              </SectionTitle>
              <div className="flex gap-6">
                <SubscriptionCard
                  main={false}
                  header={"Тестовий період"}
                  footer={<><p><StrongBlue>0%</StrongBlue></p><p>з доходу за місяць</p></>}
                >
                  <SubscriptionCardMenuItem imageSrc="/check.png" size={12}>
                    <p>Період дії <StrongBlue>1 місяць</StrongBlue></p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem imageSrc="/close.png" size={9}>
                    <p>Можливість налаштувати</p>
                    <p>робота самостійно або</p>
                    <p>з експертом</p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem imageSrc="/close.png" size={9}>
                    <p>Супровід і підтримка</p>
                  </SubscriptionCardMenuItem>
                  <SubscriptionCardMenuItem bottomBorder={true} imageSrc="/close.png" size={9}>
                    <p>Абонентська плата</p>
                  </SubscriptionCardMenuItem>
                </SubscriptionCard>
                <SubscriptionCard
                  header={"Платна підписка"}
                  footer={<><p><StrongBlue>10%</StrongBlue></p><p>з доходу за місяць</p></>}
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
            <section className="flex-col bg-blue-950 items-center py-20">
              <SectionTitle>
                <p className="font-medium text-2xl"><StrongWhite>Щоб почати заробляти разом з Matcher</StrongWhite></p>
                <p className="font-medium text-xl text-white">потрібно здійснити декілька простих кроків</p>
              </SectionTitle>
              <div className="flex justify-center gap-4">
                <StartEarnCard stepNumber="1." imageSrc="/pen.png">
                  <p><strong>Пройти реєстрацію</strong> і дочекатись</p>
                  <p>появи токену</p>
                </StartEarnCard>
                <StartEarnCard stepNumber="2." imageSrc="/deal.png">
                  <p><strong>Відкрити</strong> і поповнити <strong>рахунок</strong> в </p>
                  <p><strong>брокера</strong></p>
                  <div className="flex">
                    <Image
                      className="object-contain"
                      src="/info.png"
                      width={15}
                      height={15}
                      alt="..."
                    ></Image>
                    <p className="pl-2 text-sky-700">Обирайте перевірених брокерів</p>
                  </div>
                </StartEarnCard>
                <StartEarnCard stepNumber="3." imageSrc="/development.png">
                  <p><strong>Скачати і встановити</strong> робота по</p>
                  <p>інструкції в текстовому</p>
                  <p>документі, який буде з роботом</p>
                </StartEarnCard>
              </div>
            </section>
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
