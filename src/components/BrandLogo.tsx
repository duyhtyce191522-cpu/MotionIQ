import Image from 'next/image';

interface BrandLogoProps {
  size: number;
  className?: string;
}

export default function BrandLogo({ size, className }: BrandLogoProps) {
  return (
    <Image
      src="/images/motioniq-logo.png"
      alt="Logo MotionIQ"
      width={size}
      height={size}
      unoptimized
      className={className}
      style={{ width: size, height: size, objectFit: 'contain' }}
      priority
    />
  );
}
