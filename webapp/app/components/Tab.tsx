import { ITab } from "../page";


const Tab = ({ tab, setAсtiveTab, activeTab }: {
  tab: ITab, setAсtiveTab: (arg0: ITab) => void, activeTab: ITab
}) => {

  return (
    <li className="mr-2 cursor-pointer" key={tab.title} onClick={() => setAсtiveTab(tab)}>
      <a className={`inline-block p-4 pt-0 border-b-2 rounded-t-lg text-lg ${tab.title === activeTab.title ?
        "text-blue-500 border-blue-500 active dark:text-blue-500 dark:border-blue-500 font-medium" :
        "border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 font-normal"}`}>
        {tab.title}
      </a>
    </li>
  );
};

export default Tab;
