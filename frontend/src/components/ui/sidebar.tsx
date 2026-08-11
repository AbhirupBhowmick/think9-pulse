'use client';

import * as React from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { PanelLeft } from "lucide-react";

function cn(...inputs: any[]) {
  return twMerge(clsx(inputs));
}

interface SidebarContextValue {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  toggleSidebar: () => void;
}

const SidebarContext = React.createContext<SidebarContextValue | undefined>(undefined);

export function useSidebar() {
  const context = React.useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider");
  }
  return context;
}

export function SidebarProvider({
  children,
  defaultOpen = true,
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { defaultOpen?: boolean }) {
  const [open, setOpen] = React.useState(defaultOpen);

  const toggleSidebar = React.useCallback(() => {
    setOpen((prev) => !prev);
  }, []);

  return (
    <SidebarContext.Provider value={{ open, setOpen, toggleSidebar }}>
      <div
        className={cn("flex min-h-screen w-full bg-[#0B0F17] text-slate-100 font-sans antialiased", className)}
        {...props}
      >
        {children}
      </div>
    </SidebarContext.Provider>
  );
}

export function Sidebar({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  const { open } = useSidebar();

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-30 flex flex-col bg-[#0B0F17] border-r border-[#1E293B] transition-all duration-300 ease-in-out",
        open ? "w-56" : "w-16",
        className
      )}
      {...props}
    >
      {children}
    </aside>
  );
}

export function SidebarHeader({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("p-4 border-b border-[#1E293B] flex items-center justify-between", className)} {...props}>
      {children}
    </div>
  );
}

export function SidebarContent({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("flex-1 overflow-y-auto p-3 space-y-4", className)} {...props}>
      {children}
    </div>
  );
}

export function SidebarGroup({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("space-y-1", className)} {...props}>
      {children}
    </div>
  );
}

export function SidebarMenu({ className, children, ...props }: React.HTMLAttributes<HTMLUListElement>) {
  return (
    <ul className={cn("space-y-1 list-none p-0 m-0", className)} {...props}>
      {children}
    </ul>
  );
}

export function SidebarMenuItem({ className, children, ...props }: React.HTMLAttributes<HTMLLIElement>) {
  return (
    <li className={cn("list-none", className)} {...props}>
      {children}
    </li>
  );
}

export function SidebarMenuButton({
  className,
  isActive,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { isActive?: boolean }) {
  const { open } = useSidebar();

  return (
    <button
      className={cn(
        "w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer",
        isActive
          ? "bg-[#1E293B] text-emerald-400 border border-emerald-500/30 shadow-sm"
          : "text-slate-400 hover:text-slate-200 hover:bg-[#151E2E]",
        !open && "justify-center px-0",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}

export function SidebarFooter({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("p-4 border-t border-[#1E293B] bg-[#0B0F17]", className)} {...props}>
      {children}
    </div>
  );
}

export function SidebarTrigger({ className, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const { toggleSidebar } = useSidebar();

  return (
    <button
      onClick={toggleSidebar}
      className={cn(
        "p-2 text-slate-400 hover:text-slate-200 hover:bg-[#1E293B] rounded-lg transition-colors cursor-pointer",
        className
      )}
      {...props}
    >
      <PanelLeft className="w-4 h-4" />
    </button>
  );
}

export function SidebarInset({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  const { open } = useSidebar();

  return (
    <div
      className={cn(
        "flex-1 flex flex-col transition-all duration-300 min-h-screen",
        open ? "ml-56" : "ml-16",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
