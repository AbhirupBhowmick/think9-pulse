import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: any[]) {
  return twMerge(clsx(inputs));
}

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg text-xs font-bold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 disabled:pointer-events-none disabled:opacity-50 cursor-pointer",
  {
    variants: {
      variant: {
        default: "bg-emerald-500 text-slate-950 hover:bg-emerald-600 shadow-md shadow-emerald-950/40",
        secondary: "bg-[#1E293B] text-slate-200 hover:bg-[#334155] border border-slate-700",
        outline: "border border-[#1E293B] bg-[#111827] hover:bg-[#151E2E] text-slate-300",
        amber: "bg-amber-500/10 text-amber-400 border border-amber-500/30 hover:bg-amber-500/20",
        rose: "bg-rose-500/10 text-rose-400 border border-rose-500/30 hover:bg-rose-500/20",
        ghost: "hover:bg-[#1E293B] hover:text-slate-100 text-slate-400",
        link: "text-emerald-400 underline-offset-4 hover:underline p-0",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3 text-[11px]",
        lg: "h-11 px-6 text-sm font-extrabold",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
