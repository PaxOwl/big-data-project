! project.f90
program main

    implicit none

    integer(kind=8) :: io, i, j, nd_nline, nd_node, start_node, end_node, K
    character(len=32) :: datafile
    real(kind=8) :: alpha
    integer(kind=8), allocatable :: network_data(:, :), A(:, :), k_in(:), k_out(:)
    real(kind=8), allocatable :: S(:, :), v(:) , G(:, :), P(:, :), P0(:, :), tempP(:, :)

    datafile = "network_data.dat"
    call countLines

    allocate(network_data(nd_nline, 2))

    call buildNetworkData

    allocate(A(nd_node, nd_node))
    allocate(k_in(nd_node))
    allocate(k_out(nd_node))
    allocate(S(nd_node, nd_node))
    allocate(v(nd_node))
    allocate(G(nd_node, nd_node))
    allocate(P(nd_node, 1))
    allocate(P0(nd_node, 1))
    allocate(tempP(nd_node, 1))

    alpha = .85
    
    call buildNetworkStructure
    call buildStochasticMatrix
    call buildGoogleMatrix

    call saveArray
    contains

    subroutine countLines

        implicit none

        open(unit=111, file=datafile)
        nd_nline = 0

        do
            read(111, *, iostat=io)
            if (io < 0) then
                exit
            end if
            nd_nline = nd_nline + 1
        enddo

        close(111)

    end subroutine countLines


    subroutine buildNetworkData

        implicit none

        open(unit=111, file=datafile)

        do i = 1, nd_nline
            read(111, *, iostat=io) network_data(i, 1), network_data(i, 2)
        end do

        nd_node = network_data(nd_nline, 1)

    end subroutine buildNetworkData


    subroutine buildNetworkStructure

        implicit none

        do i = 1, nd_node
            do j = 1, nd_node
                A(i, j) = 0
            end do
        end do

        do i = 1, nd_nline
            start_node = network_data(i, 2)
            end_node = network_data(i, 1)
            A(start_node, end_node) = 1
        end do

    end subroutine buildNetworkStructure


    subroutine buildStochasticMatrix

        implicit none

        do j = 1, nd_node
            k_in(j) = 0
            k_out(j) = 0
            do i = 1, nd_node
                k_in(j) = k_in(j) + A(j, i)
                k_out(j) = k_out(j) + A(i, j)
            end do
        end do

        do i = 1, nd_node
            do j = 1, nd_node
                if (k_out(j) == 0) then
                    S(i, j) = 1. / real(nd_node, 8)
                else
                    S(i, j) = A(i, j) / real(k_out(j), 8)
                end if
            end do
        end do
        print *, k_in
        print *, k_out

    end subroutine buildStochasticMatrix


    subroutine buildGoogleMatrix

        implicit none

        do i = 1, nd_node
            v(i) = 1 / real(nd_node, 8)
            do j = 1, nd_node
                G(i, j) = alpha * S(i, j) + (1 - alpha) * v(i)
            end do
        end do

    end subroutine buildGoogleMatrix


    subroutine saveArray

        implicit none

        open(unit=222, file="S.dat", iostat=io)
        do i=1, nd_node
            do j=1, nd_node
                write(unit=222, fmt="(F8.4)", advance='no') S(i, j)
            end do
            write(unit=222, fmt="(A4)") ''
        end do
        close(222)

        open(unit=222, file="G.dat", iostat=io)
        do i=1, nd_node
            do j=1, nd_node
                write(unit=222, fmt="(F8.4)", advance='no') G(i, j)
            end do
            write(unit=222, fmt="(A4)") ''
        end do
        close(222)

        open(unit=222, file="P.dat", iostat=io)
        do i=1, nd_node
            write(unit=222, fmt="(F8.4)", advance='no') P(i, 1)
            write(unit=222, fmt="(A4)") ''
        end do
        close(222)

    end subroutine saveArray


end program main
