subroutine mph_FillVars(s,pf,crv,thco,cprs,visc,rho1x,rho1y,rho2x,rho2y,al1x,al1y,al2x,al2y,nrmx,nrmy,smhv,smrh)

#include "Solver.h"

    use Multiphase_data
    use Grid_data, ONLY: gr_dx,gr_dy

    implicit none
    real,intent(inout),dimension(Nxb+2,Nyb+2) :: pf,thco,cprs,visc,crv,rho1x,rho1y,&
                                                 rho2x,rho2y,al1x,al1y,al2x,al2y,nrmx,nrmy,smhv,smrh
                                                            

    real, intent(in), dimension(:,:) :: s

    integer :: i,j

    real :: rPhiXN,rPhiXE,rPhiXS,rPhiXW, &
            rPhiYN,rPhiYE,rPhiYS,rPhiYW, &
            rMagN,rMagE,rMagS,rMagW

    real :: a1,a2

    double precision :: sp

    real, parameter :: eps = 1E-13

    real, parameter :: pi  = acos(-1.0)

     mph_crmx = 0.
     mph_crmn = 0.

     crv = 0.
     do j = 2,Nyb+1
       do i = 2,Nxb+1

              !----------------------------------------------------
              !- kpd - 2 phi gradients per face method
              !----------------------------------------------------
              !        X - Location

              rPhiXE = 1./gr_dx*(s(i+1,j)-s(i,j)  )
              rPhiXW = 1./gr_dx*(s(i,j)  -s(i-1,j))
              rPhiXN = 1./4./gr_dx * ( (s(i+1,j+1) - s(i-1,j+1)) &
                                  + (s(i+1,j)   - s(i-1,j)  ) )
              rPhiXS = 1./4./gr_dx * ( (s(i+1,j)   - s(i-1,j)  ) &
                                  + (s(i+1,j-1) - s(i-1,j-1)) )
             !        Y - Location
              rPhiYN = 1./gr_dy*(s(i,j+1)-s(i,j)  )
              rPhiYS = 1./gr_dy*(s(i,j)  -s(i,j-1))
              rPhiYE = 1./4./gr_dy * ( (s(i+1,j+1) - s(i+1,j-1)) &
                                  + (s(i,j+1)   - s(i,j-1)  ) )
              rPhiYW = 1./4./gr_dy * ( (s(i,j+1)   - s(i,j-1)  ) &
                                  + (s(i-1,j+1) - s(i-1,j-1)) )
              !----------------------------------------------------

              rMagE = sqrt( rPhiXE**2. + rPhiYE**2. ) + eps
              rMagW = sqrt( rPhiXW**2. + rPhiYW**2. ) + eps
              rMagN = sqrt( rPhiXN**2. + rPhiYN**2. ) + eps
              rMagS = sqrt( rPhiXS**2. + rPhiYS**2. ) + eps


              crv(i,j) = 1./gr_dx * (rPhiXE/rMagE - rPhiXW/rMagW) &
                         + 1./gr_dy * (rPhiYN/rMagN - rPhiYS/rMagS)
              !----------------------------------------------------

        end do
     end do

     sp = 3.0*gr_dx

     do j=1,Nyb+2
      do i=1,Nxb+2

        if(abs(s(i,j)) .le. sp) then ! Symmetric smearing - AD
        !if(abs(s(i,j)) .le. sp .and. s(i,j) .le. 0.0) then ! Asymmetric smearing - AD

         smhv(i,j) = 0.5 + s(i,j)/(2*sp) + sin(2*pi*s(i,j)/(2*sp))/(2*pi)

        else

          if(s(i,j) .gt. 0.0) then

               smhv(i,j) = 1.0

          else

               smhv(i,j) = 0.0

          end if

        end if


      end do
    end do

    smrh =  (mph_rho2/mph_rho2) + (mph_rho1/mph_rho2 - mph_rho2/mph_rho2) * smhv
    smrh =  1./smrh

    pf   = 0.
    pf   = (sign(1.0,s)+1.0)/2.0

    visc = (mph_vis2/mph_vis2)   + (mph_vis1/mph_vis2   - mph_vis2/mph_vis2)   * smhv

    thco = (mph_thco2/mph_thco2) + (mph_thco1/mph_thco2 - mph_thco2/mph_thco2) * pf 

    cprs = (mph_cp2/mph_cp2)     + (mph_cp1/mph_cp2     - mph_cp2/mph_cp2)     * pf

    rho1x = 0.
    rho2x = 0.
    al1x  = 0.
    al2x  = 0.

    do j = 2,Nyb+1
      do i = 2,Nxb+1

         a1 = (pf(i-1,j) + pf(i,j)) / 2.
         a2 = pf(i-1,j)  /abs(pf(i-1,j)  +eps) * &
              pf(i,j)/abs(pf(i,j)+eps)

         rho1x(i,j) = a1*a2/(mph_rho1/mph_rho2)
         rho2x(i,j) = (1. - a1*a2)/(mph_rho2/mph_rho2)

         al1x(i,j) = a1*a2/((mph_thco1/mph_cp1)/(mph_thco2/mph_cp2))
         al2x(i,j) = (1. - a1*a2)/((mph_thco2/mph_cp2)/(mph_thco2/mph_cp2))

      end do
    end do

    rho1y = 0.
    rho2y = 0.
    al1y  = 0.
    al2y  = 0.

    do j = 2,Nyb+1
       do i = 2,Nxb+1

         a1 = (pf(i,j-1) + pf(i,j)) / 2.
         a2 = pf(i,j-1)  /abs(pf(i,j-1)  +eps) * &
                pf(i,j)/abs(pf(i,j)+eps)

         rho1y(i,j) = a1*a2/(mph_rho1/mph_rho2)
         rho2y(i,j) = (1. - a1*a2)/(mph_rho2/mph_rho2)

         al1y(i,j) = a1*a2/((mph_thco1/mph_cp1)/(mph_thco2/mph_cp2))
         al2y(i,j) = (1. - a1*a2)/((mph_thco2/mph_cp2)/(mph_thco2/mph_cp2))

       end do
    end do

    nrmx(2:Nxb+1,2:Nyb+1) = ((s(3:Nxb+2,2:Nyb+1) - s(1:Nxb,2:Nyb+1))/2./gr_dx)/ &
                       sqrt(((s(3:Nxb+2,2:Nyb+1) - s(1:Nxb,2:Nyb+1))/2./gr_dx)**2 &
                          + ((s(2:Nxb+1,3:Nyb+2) - s(2:Nxb+1,1:Nyb))/2./gr_dy)**2 )

    nrmy(2:Nxb+1,2:Nyb+1) = ((s(2:Nxb+1,3:Nyb+2) - s(2:Nxb+1,1:Nyb))/2./gr_dy)/ &
                       sqrt(((s(3:Nxb+2,2:Nyb+1) - s(1:Nxb,2:Nyb+1))/2./gr_dx)**2 &
                          + ((s(2:Nxb+1,3:Nyb+2) - s(2:Nxb+1,1:Nyb))/2./gr_dy)**2 )

end subroutine mph_FillVars
