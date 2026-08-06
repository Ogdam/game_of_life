import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import SideBar from './sidebar'
import { useSimulationStore } from '../stores/store'

describe('SideBar', () => {
  beforeEach(() => {
    useSimulationStore.setState(useSimulationStore.getInitialState(), true)
  })

  it('displays the title and the current generation', () => {
    useSimulationStore.getState().setGeneration(42)
    render(<SideBar />)

    expect(screen.getByText('Cornwell Game Of Life')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
  })

  it('renders the controls section', () => {
    render(<SideBar />)
    expect(screen.getByRole('button', { name: /start/i })).toBeInTheDocument()
  })
})
