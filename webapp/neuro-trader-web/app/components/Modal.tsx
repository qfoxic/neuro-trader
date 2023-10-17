"use client"

import { useRouter } from 'next/navigation';
import { useState } from "react";
import { ITab } from '../page';
import Tab from './Tab';


const Modal = ({ defaultTab, tabs }:
  { defaultTab: ITab, tabs: ITab[] }) => {
  const [activeTab, setAсtiveTab] = useState(defaultTab);
  const router = useRouter();

  return (
    <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
      <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div className="flex min-h-full items-end justify-center p-4 text-center items-center sm:p-0">
          <div className="relative transform overflow-hidden rounded-lg bg-white text-center shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-sm">
            <div className="px-8 py-4">
              <div className="text-gray-600 text-xl text-right" onClick={() => router.push('/')}>
                ✕
              </div>
              <div className="text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:text-gray-400 dark:border-gray-700">
                <ul className="flex flex-wrap -mb-px justify-center">
                  {
                    tabs.map(tab => (
                      <Tab
                        key={ tab.title}
                        tab={tab}
                        setAсtiveTab={setAсtiveTab}
                        activeTab={activeTab}
                      />
                    ))
                  }
                </ul>
              </div>
              <div className="py-4">
                {activeTab.children}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
