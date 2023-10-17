import { ITab } from "../page";


const Tab = ({ tab, setAсtiveTab, activeTab }: {
  tab: ITab, setAсtiveTab: (arg0: ITab) => void, activeTab: ITab
}) => {

  return (
    <li className="mr-2" key={tab.title} onClick={() => setAсtiveTab(tab)}>
      <a className={`inline-block p-4 pt-0 border-b-2 rounded-t-lg ${tab.title === activeTab.title ?
        "text-blue-600 border-blue-600 active dark:text-blue-500 dark:border-blue-500" :
        "border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300"}`}>
        {tab.title}
      </a>
    </li>
  );
};

export default Tab;
